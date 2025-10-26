# HotSpots

**Interactive Wi-Fi Heatmap Visualization Platform**

A modern web application that visualizes network usage patterns through interactive 3D heatmaps, showcasing real-time Wi-Fi access point data from Dartmouth College and Hong Kong University Library.

![HotSpots Banner](src/assets/Resized_20251026_004217-removebg-preview.png)

---

## Features

- **Interactive 3D Visualizations**: Explore campus-wide Wi-Fi heatmaps with pan, zoom, and rotation capabilities
- **Multi-Location Data**: Compare network usage patterns across different geographical locations
- **Real-Time Insights**: Visualize access point distribution and network traffic intensity
- **Responsive Design**: Seamlessly adapts to desktop, tablet, and mobile devices
- **Modern UI**: Clean, light neutral theme with smooth animations and glassmorphism effects

---

## 📊 Data Visualizations

### Dartmouth Data

Interactive campus-wide Wi-Fi heatmap showing access point distribution across Dartmouth College campus. Visualize network density and usage patterns in real-time.

### Hong Kong Data

3D multi-floor visualization of HKU Library Wi-Fi traffic, displaying network usage intensity across multiple building levels with interactive controls.

---

## 🛠️ Tech Stack

- **Frontend**: React 19.1.1
- **Build Tool**: Vite 7.1.7
- **Styling**: CSS3 with Custom Properties
- **Data Visualization**: Plotly.js (3D interactive graphs)
- **Navigation**: React Anchor Link Smooth Scroll
- **Deployment**: Production-ready build system

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd HotSpots
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:5173
   ```

---

## 📦 Build for Production

```bash
npm run build
```

The optimized production build will be created in the `dist` folder.

### Preview Production Build

```bash
npm run preview
```

---

## 🌐 Deployment

Deploy your HotSpots website to any static hosting platform:

### Vercel (Recommended)

```bash
npm install -g vercel
vercel login
vercel --prod
```

### Netlify

```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=dist
```

### GitHub Pages

```bash
npm install --save-dev gh-pages
npm run deploy
```

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

---

## 📁 Project Structure

```
HotSpots/
├── public/
│   ├── hku_library_3d_floors.html      # Hong Kong 3D heatmap
│   ├── interactive_campus_heatmap.html # Dartmouth campus heatmap
│   └── new-dartmouth-campus-map.jpg    # Campus base map
├── src/
│   ├── components/
│   │   ├── Navbar/           # Navigation component
│   │   ├── Desc/             # Home/Hero section
│   │   ├── DartmouthData/    # Dartmouth visualization
│   │   ├── HongKongData/     # Hong Kong visualization
│   │   ├── Footer/           # Footer component
│   │   └── Background/       # Animated background
│   ├── assets/               # Images and static assets
│   ├── index.css             # Global styles
│   ├── App.jsx               # Main app component
│   └── main.jsx              # Entry point
├── package.json
└── vite.config.js
```

---

## 🎨 Design System

### Color Palette

- **Primary**: `#6b7280` (Gray)
- **Secondary**: `#9ca3af` (Light Gray)
- **Accent**: `#d4af37` (Gold)
- **Background**: `#f9fafb` (Light)
- **Text**: `#1f2937` (Dark Gray)

### Typography

- **Headings**: Poppins (800 weight)
- **Body**: Inter (400-600 weight)

### Key Features

- Glassmorphism effects with backdrop blur
- Smooth gradient transitions
- Responsive breakpoints at 768px
- Custom scrollbar styling

---

## 📱 Responsive Design

- **Desktop**: Full-featured experience with large visualizations
- **Tablet**: Optimized layout with adjusted spacing
- **Mobile**: Touch-friendly interface with collapsible navigation

---

## 🔧 Scripts

| Command           | Description              |
| ----------------- | ------------------------ |
| `npm run dev`     | Start development server |
| `npm run build`   | Build for production     |
| `npm run preview` | Preview production build |
| `npm run lint`    | Run ESLint               |

---

## 📊 Data Sources

### Dartmouth College Dataset

- Campus-wide Wi-Fi access point distribution
- Real-time network usage patterns
- Location: Dartmouth College Campus

### Hong Kong University Library

- Multi-floor Wi-Fi traffic visualization
- 3D building representation
- Location: HKU Library, Hong Kong

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Team

Built with passion for data visualization and network analytics.

---

## 📞 Contact

For questions or feedback, visit the contact section on our website.

---

## 🙏 Acknowledgments

- Dartmouth College for campus network data
- Hong Kong University for library Wi-Fi data
- React and Vite communities for excellent tools
- Plotly for interactive visualization capabilities

---

## 📈 Future Enhancements

- [ ] Real-time data updates
- [ ] More campus locations
- [ ] Historical data comparison
- [ ] User-uploaded heatmaps
- [ ] Advanced filtering options
- [ ] Export visualization data
- [ ] Dark mode toggle

---

**Made with ❤️ for better network visualization**
