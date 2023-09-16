import { useState, useEffect, useContext } from 'react'
import { Routes, Route, useNavigate, redirect } from 'react-router-dom'
import appLogo from './../assets/logo.svg'
import '../styles/App.css'
import { UserProvider } from '../contexts/UserContext'

import Home from './pages/Home'
import NewOwners from './pages/NewOwners'
import Shelter from './pages/Shelter'
import Login from './pages/Login'
import Register from './pages/Register'
import Logout from './pages/Logout'
import Profile from './pages/Profile'
import MyPets from './pages/MyPets'
import MyFriends from './pages/MyFriends'
import MyFriend from './pages/MyFriend'
import Thread from './pages/Thread'

import Header from './Header'
import Footer from './Footer'

function App() {

  return (
    <>
      <UserProvider>
        <Header />
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/newowners" element={<NewOwners />} />
          <Route path="/shelter" element={<Shelter />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/mypets" element={<MyPets />} />
          <Route path="/friends" element={<MyFriends />} />
          <Route path="/profile/:username" element={<MyFriend />} />
          <Route path="/thread/:username" element={<Thread />} />
        </Routes>
        <Footer />
      </UserProvider>
    </>
  )
}

export default App
