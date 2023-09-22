import {useState, useEffect, useContext} from "react"
import {Link, Navigate} from "react-router-dom"



export default function Home () {
    return (
        <div>
            <h1>Home</h1>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
        </div>
    )
}
