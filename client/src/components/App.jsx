import { useState, useEffect, useContext } from 'react'
import { Routes, Route, useNavigate, redirect } from 'react-router-dom'
import appLogo from './../assets/logo.svg'
import '../styles/App.css'
import { UserProvider } from '../contexts/UserContext'

import Home from './pages/Home'
import About from './pages/About'
import NewOwners from './pages/NewOwners'
import Shelter from './pages/Shelter'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Logout from './pages/Logout'
import Profile from './pages/Profile'
import MyPets from './pages/MyPets'
import MyFriends from './pages/MyFriends'

import Header from './Header'
import Footer from './Footer'


import reactLogo from './../assets/react.svg'
import viteLogo from '/vite.svg'

function App() {
  const navigate = useNavigate()
  const [count, setCount] = useState(0)

  return (
    <>
      <UserProvider>
        <Header />
        {/* <div>
          <a href="https://vitejs.dev">
            <img src={viteLogo} className="logo" alt="Vite logo" />
          </a>
          <a href="https://react.dev">
            <img src={reactLogo} className="logo react" alt="React logo" />
          </a>
        </div> */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/newowners" element={<NewOwners />} />
          <Route path="/shelter" element={<Shelter />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/logout" element={<Logout />} navigate={navigate} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/mypets" element={<MyPets />} />
          <Route path="/myfriends" element={<MyFriends />} />
        </Routes>
        <Footer />
      </UserProvider>
    </>
  )
}

export default App
