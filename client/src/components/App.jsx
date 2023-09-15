import { useState, useEffect, useContext } from 'react'
import { Routes, Route, useNavigate, redirect } from 'react-router-dom'
import appLogo from './../assets/logo.svg'
import '../styles/App.css'
import { UserProvider } from '../contexts/UserContext'

import Pound from './pages/Pound'
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
  const [count, setCount] = useState(0)

  return (
    <>
      <UserProvider>
        <Header />
        <div>
          <a href="https://vitejs.dev" target="_blank">
            <img src={viteLogo} className="logo" alt="Vite logo" />
          </a>
          <a href="https://react.dev" target="_blank">
            <img src={reactLogo} className="logo react" alt="React logo" />
          </a>
        </div>
        <h1>Vite + React</h1>
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
          <p>
            Edit <code>src/App.jsx</code> and save to test HMR
          </p>
        </div>
        <p className="read-the-docs">
          Click on the Vite and React logos to learn more
        </p>
        <Routes>
          <Route path="/pound" element={<Pound />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/logout" element={<Logout />} />
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
