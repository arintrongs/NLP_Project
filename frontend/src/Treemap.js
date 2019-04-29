import React from 'react'
import * as d3 from 'd3'

class Treemap extends React.Component {
  static color = d3.schemeCategory10

  render() {
    const treemap = d3.treemap()
    // .size([960, 500])
    // .sticky(true)
    // .value(d => d.size)(this.props.root)

    return (
      <div style={{ position: 'relative', width: '960px', height: '500px', left: '10px', top: '10px' }}>
        {treemap.map(n => (
          <div
            className="node"
            style={{
              background: n.children ? Treemap.color(n.name) : null,
              left: `${n.x}px`,
              top: `${n.y}px`,
              width: `${Math.max(0, n.dx - 1)}px`,
              height: `${Math.max(0, n.dy - 1)}px`
            }}
          >
            {n.children ? null : n.name}
          </div>
        ))}
      </div>
    )
  }
}

export default Treemap
