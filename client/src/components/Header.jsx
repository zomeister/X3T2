import { useState, useContext, useEffect } from "react"
import { Link } from "react-router-dom"
import { UserContext } from "../contexts/UserContext"
import "../styles/Header.css"

export default function Header () {
    const { user, setUser } = useContext(UserContext)
    const [count, setCount] = useState(0)
    const [error, setError] = useState(null)

    const authorizeUser = () => {
        fetch('api/check_session')
        .then(res =>  {
             if (res.status === 200) {
                 return res.json()
             } else {
                setError('Session expired')
             }
         })
        .then(data => setUser(data))
        .catch(err => console.log(err))
    }
    
    useEffect(() => {
        user ? authorizeUser : null
    }, [user])

    return(
        <header>
            <h2 id="app-title">X3T2</h2>
            <div id="nav-links">
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
                {user
                ? <>
                    <Link to="/shelter">shelter</Link>
                    <Link to="/newowners">(newowners)</Link>
                    <Link to="/mypets">My Pets</Link>
                    <Link to="/myfriends">My Friends</Link>
                    <Link to="/profile">Profile</Link>
                </> : <>
                    <Link to="/shelter">shelter</Link>
                    <Link to="/newowners">(newowners)</Link>
                </>
                }
            </div>
            <div id="auth-links">
                {user == null 
                    ? <>
                        <Link to="/login">Login</Link>
                        <Link to="/signup">Signup</Link>
                    </> 
                    : <>
                        <Link to="/logout">Logout</Link>
                    </>
                }
                {/* <button onClick={() => setCount(count => count+1)}>Count: {count}</button> */}
            </div>
        </header>
    )
}