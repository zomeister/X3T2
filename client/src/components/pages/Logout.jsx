import { useState, useContext, useEffect} from "react"
import { Navigate } from "react-router-dom"
import { UserContext } from "../../contexts/UserContext"

export default function Logout() {
    const { user, setUser } = useContext(UserContext)
    function logout() {
        fetch('/api/logout', {method: 'DELETE'})
       .then((res) => {
          if (res.ok) {
            setUser(null)
            // console.log(user)
            // return redirect("/login")
          }
       })
    }

    useEffect(() => {
        logout()
    })

    return (
        <div>
            <h1>Logout</h1>
            {user ? <p>error logging out</p> : <Navigate to="/" replace={true} />}
        </div>
    )
}