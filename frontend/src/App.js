import React from 'react'
import { Treemap } from 'react-vis'
import { Card, Divider, Button, Drawer, Select, Transfer } from 'antd'
import axios from 'axios'
import _ from 'lodash'
import '../node_modules/react-vis/dist/style.css'
import './App.css'

const Option = Select.Option

class App extends React.Component {
  state = {
    data: [],
    value: 1000,
    loading: false,
    visible: false,
    selectedKeys: [],
    targetKeys: [],
    selectedPublisher: 'standard',
    selectedData: []
  }
  async componentDidMount() {
    this.setState({ loading: true })
    const { data } = await axios.get(`http://localhost:5000/getlist?publisher=standard`)
    this.setState({
      data: data.map(d => ({ ...d, headline: _.replace(d.headline, /"/g, '') })),
      loading: false
    })
  }
  handlePublisherChange = async val => {
    try {
      this.setState({ loading: true })
      const { data } = await axios.get(`http://localhost:5000/getlist?publisher=${val}`)
      this.setState({
        data: data.map(d => ({ ...d, headline: _.replace(d.headline, /"/g, '') })),
        selectedPublisher: val,
        selectedKeys: [],
        targetKeys: [],
        loading: false
      })
    } catch (e) {
      this.setState({ loading: false })
    }
  }

  onClose = () => {
    this.setState({ visible: false })
  }
  showDrawer = () => {
    this.setState({ visible: true })
  }
  handleSelectChange = (sourceSelectedKeys, targetSelectedKeys) => {
    this.setState({ selectedKeys: [...sourceSelectedKeys, ...targetSelectedKeys] })
  }
  handleChange = (nextTargetKeys, direction, moveKeys) => {
    this.setState({ targetKeys: nextTargetKeys })
  }
  handleUpdate = () => {
    const colors = [
      '#8dd3c7',
      '#ffffb3',
      '#bebada',
      '#fb8072',
      '#80b1d3',
      '#fdb462',
      '#b3de69',
      '#fccde5',
      '#d9d9d9',
      '#bc80bd',
      '#ccebc5',
      '#ffed6f'
    ].sort((a, b) => Math.random())
    let data = []
    for (let idx of this.state.targetKeys) {
      data.push(this.state.data[idx])
    }
    this.setState({ selectedData: data.map((d, idx) => ({ ...d, color: colors[idx % colors.length] })) })
  }
  renderDrawer = () => {
    return (
      <Drawer title="Settings" placement="top" closable={false} onClose={this.onClose} visible={this.state.visible} height={600}>
        <div className="panel">
          <div className="publisher">
            Select Publisher :<br />
            <Select style={{ width: '100%' }} value={this.state.selectedPublisher} onChange={this.handlePublisherChange}>
              <Option key="1" value="standard">
                The Standard
              </Option>
              <Option key="2" value="thaipbs">
                ThaiPBS
              </Option>
              <Option key="3" value="ch3">
                Ch3
              </Option>
              <Option key="4" value="nation">
                Nation
              </Option>
            </Select>
          </div>
          <div className="transfer">
            <Transfer
              titles={['Source', 'Target']}
              dataSource={this.state.data.slice(0, 100).map((val, idx) => ({
                key: idx,
                title: val.headline
              }))}
              targetKeys={this.state.targetKeys}
              selectedKeys={this.state.selectedKeys}
              onChange={this.handleChange}
              onSelectChange={this.handleSelectChange}
              onScroll={this.handleScroll}
              listStyle={{
                width: 300,
                height: 450
              }}
              render={item => item.title}
            />
          </div>
          <div className="button-container">
            <Button onClick={this.handleUpdate} icon="upload" type="primary">
              Update
            </Button>
          </div>
        </div>
      </Drawer>
    )
  }
  render() {
    const totalPredictedView = this.state.selectedData.reduce((acc, val) => acc + parseInt(val['Predicted views']), 0)
    const totalActualView = this.state.selectedData.reduce((acc, val) => acc + parseInt(val['Actual views']), 0)
    const predicted = {
      color: '#9E9E9E',
      children: this.state.selectedData.map(e => ({
        title: e.headline,
        size: parseInt(e['Predicted views']),
        color: e.color,
        style: { fontSize: 8 + (parseInt(e['Predicted views']) / totalPredictedView) * 100 }
      }))
    }
    const actual = {
      color: '#9E9E9E',
      children: this.state.selectedData.map(e => ({
        title: e.headline,
        size: parseInt(e['Actual views']),
        color: e.color,
        style: { fontSize: 8 + (parseInt(e['Actual views']) / totalActualView) * 100 }
      }))
    }
    return (
      <div className="App">
        <div className="header">
          <div className="title">News Headline Proportion Generator</div>
          <Button type="primary" icon="setting" onClick={this.showDrawer}>
            Open Setting
          </Button>
        </div>

        <Divider />
        <div className="container">
          <div className="views item">
            <Card title="Predicted Views" style={{ width: '100%' }}>
              <div className="views-item">
                <div className="title">
                  <b>Title</b>
                </div>
                <div className="view">
                  <b>View</b>
                </div>
              </div>
              {this.state.selectedData.map((e, idx) => (
                <div key={idx} className="views-item">
                  <div className="title">{e.headline}</div>
                  <div className="view">{parseInt(e['Predicted views'])}</div>
                </div>
              ))}
            </Card>
          </div>
          <div className="predicted item">
            <h2>======= Predicted =======</h2>
            <Treemap
              key={Math.random()}
              title="Predicted"
              height={842}
              width={545}
              data={predicted}
              padding={10}
              colorType={'literal'}
              animation={true}
            />
          </div>
          .
          <div className="real item">
            <h2>======= Actual =======</h2>
            <Treemap
              key={Math.random()}
              title="Predicted"
              height={842}
              width={545}
              data={actual}
              padding={10}
              colorType={'literal'}
              animation={true}
            />
          </div>
          <div className="views item">
            <Card title="Actual Views" style={{ width: '100%' }}>
              <div className="views-item">
                <div className="title">
                  <b>Title</b>
                </div>
                <div className="view">
                  <b>View</b>
                </div>
              </div>
              {this.state.selectedData.map((e, idx) => (
                <div key={idx} className="views-item">
                  <div className="title">{e.headline}</div>
                  <div className="view">{parseInt(e['Actual views'])}</div>
                </div>
              ))}
            </Card>
          </div>
        </div>
        {this.renderDrawer()}
      </div>
    )
  }
}

export default App
