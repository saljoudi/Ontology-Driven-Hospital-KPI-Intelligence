# Ontology-Driven Hospital KPI Intelligence WebApp - Design Guide

## Design Philosophy

### Color Palette
- **Primary**: Clinical Blue (#2563eb) - Professional, trustworthy, healthcare-focused
- **Secondary**: Soft Teal (#0891b2) - Modern, analytical, complementary to primary
- **Accent**: Warm Amber (#f59e0b) - Highlights, warnings, attention-grabbing elements
- **Neutral**: Cool Gray (#64748b) - Text, secondary information
- **Background**: Pure White (#ffffff) - Clean, clinical, professional
- **Success**: Forest Green (#059669) - Positive KPIs, healthy metrics
- **Warning**: Sunset Orange (#ea580c) - Borderline KPIs, caution indicators
- **Critical**: Deep Red (#dc2626) - Problematic KPIs, urgent attention needed

### Typography
- **Display Font**: "Inter" - Modern, highly legible sans-serif for headings and UI elements
- **Body Font**: "Inter" - Consistent typography system for optimal readability
- **Monospace**: "JetBrains Mono" - For code, data values, and technical displays
- **Font Sizes**: 
  - Hero: 3.5rem (56px) - Main dashboard title
  - H1: 2.5rem (40px) - Section headers
  - H2: 1.875rem (30px) - Subsection headers
  - H3: 1.5rem (24px) - Component titles
  - Body: 0.875rem (14px) - Standard text (smaller for data density)
  - Small: 0.75rem (12px) - Labels, metadata

### Visual Language
- **Clinical Precision**: Clean lines, precise alignments, medical-grade accuracy
- **Data-Driven Aesthetics**: Minimal visual noise, focus on information hierarchy
- **Professional Trust**: Conservative color usage, established healthcare conventions
- **Intelligent Sophistication**: Subtle gradients, refined shadows, premium feel

## Visual Effects & Styling

### Used Libraries
- **Anime.js**: Smooth micro-interactions, KPI value transitions, node animations
- **ECharts.js**: Interactive network graphs, hierarchical visualizations, real-time charts
- **p5.js**: Dynamic background particles, organic data flow animations
- **Splitting.js**: Text reveal animations for insights and recommendations
- **Typed.js**: Typewriter effect for dynamic insights generation
- **Splide.js**: Smooth carousel for departmental KPI comparisons

### Animation & Effects
- **Network Graph Animations**: 
  - Node pulse effects for real-time updates
  - Smooth edge transitions showing relationship changes
  - Particle flow along connections representing data influence
  - Gentle floating motion for active elements

- **KPI Card Effects**:
  - Subtle glow animations for critical alerts
  - Smooth value counting animations
  - Color transition effects for status changes
  - Micro-interactions on hover and selection

- **Background Atmosphere**:
  - Subtle particle system representing data flow
  - Gentle gradient shifts based on overall hospital performance
  - Clean geometric patterns suggesting precision and order

### Header & Navigation Effect
- **Clean Clinical Header**: Minimal design with essential navigation only
- **Status Indicators**: Real-time hospital performance status with color coding
- **Smooth Transitions**: Page transitions that maintain context and flow
- **Responsive Adaptation**: Seamless experience across device sizes

### Interactive Elements
- **Hover States**: 
  - 3D tilt effects on KPI cards
  - Shadow expansion for clickable elements
  - Color intensification for network nodes
  - Smooth scale transitions (1.02x scale factor)

- **Selection States**:
  - Highlighted borders with primary blue
  - Background color shifts for active elements
  - Connection highlighting in network graphs
  - Contextual information panels

### Data Visualization Styling
- **Network Graph Design**:
  - Nodes: Circular with department icons and status colors
  - Edges: Bezier curves with thickness indicating relationship strength
  - Layout: Force-directed with semantic clustering
  - Interactions: Zoom, pan, node selection, detail overlays

- **Chart Aesthetics**:
  - Clean grid lines with minimal opacity
  - Smooth curve interpolation for trend lines
  - Color-coded data series following status palette
  - Interactive tooltips with contextual information

### Responsive Design
- **Desktop**: Full dashboard layout with all panels visible
- **Tablet**: Collapsible sidebar panels, optimized touch interactions
- **Mobile**: Stack layout with swipe navigation between views

### Accessibility Considerations
- **High Contrast**: All text maintains 4.5:1 contrast ratio minimum
- **Color Independence**: Information conveyed through multiple visual cues
- **Keyboard Navigation**: Full functionality without mouse interaction
- **Screen Reader Support**: Semantic HTML and ARIA labels

### Professional Healthcare Aesthetic
- **Clinical Precision**: Every element serves a functional purpose
- **Data Integrity**: Visual representations that maintain statistical accuracy
- **Trust Indicators**: Consistent visual language that builds confidence
- **Sophisticated Simplicity**: Complex functionality presented elegantly