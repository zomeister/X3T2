import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import OwnerCard from "../OwnerCard"

export default function MyFriends() {
    const { user } = useContext(UserContext)
    return (<p>My Friends</p>)
}