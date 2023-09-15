import { useState, useContext } from "react"

import { UserContext } from "../../contexts/UserContext"

export default function Logout() {
    const { setUser } = useContext(UserContext)
    return (
        <p>Logout</p>
    )
}