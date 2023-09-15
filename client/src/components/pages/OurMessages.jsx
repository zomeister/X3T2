import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"

export default function OurMessages() {
    const { user } = useContext(UserContext)
    return (<p>OurMessages</p>)
}