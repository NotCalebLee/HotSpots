import Desc from "./components/Desc/Desc"
import Navbar from './components/Navbar/Navbar'
import DartmouthData from './components/DartmouthData/DartmouthData'
import HongKongData from './components/HongKongData/HongKongData'
import Footer from './components/Footer/Footer'
import Background from './components/Background/Background'

function App() {
  return (
    <div>
      <Background />
      <Navbar />
      <Desc />
      <DartmouthData />
      <HongKongData />
      <Footer />
    </div>
  )
}

export default App
