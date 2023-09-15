import { useState, useContext, useEffect } from "react"
import { Link } from "react-router-dom"
import { UserContext } from "../contexts/UserContext"

export default function Header () {
    const { user, setUser } = useContext(UserContext)

    return(
        <header>Header
            <Link to="/">Home</Link>
            <Link to="/pound">(pound)</Link>
            {user == null 
                ? <>
                    <Link to="/login">Login</Link>
                    <Link to="/signup">Signup</Link>
                </> 
                : <>
                    <Link to="/profile">Profile</Link>
                    <Link to="/mypets">My Pets</Link>
                    <Link to="/myfriends">My Friends</Link>
                    <Link to="/logout">Logout</Link>
                </>
            }
        </header>
    )

}