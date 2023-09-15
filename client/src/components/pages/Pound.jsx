import { useState, useContext, useEffect } from "react"
// import { UserContext } from "../../contexts/userContext"
import PetCard from "../PetCard"

export default function Pound() {
    const [ shelterPets, setShelterPets ] = useState([])
    
    const poundPets = () => {
        fetch('api/shelter')
        .then(res => res.json())
        .then(data => setShelterPets(data))
    }

    useEffect(() => {
        poundPets()
    },[])

    return (<>
        {shelterPets.map(p => <PetCard key={p.id} pet={p}/>)}
    </>)
}