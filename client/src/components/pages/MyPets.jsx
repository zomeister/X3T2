import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import PetCard from "../PetCard"

export default function MyPets() {
    const { user } = useContext(UserContext)
    return (<p>MyPets</p>)
}