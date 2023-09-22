import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import PetCard from "../PetCard"
import AddPet from "../AddPet"

export default function Shelter({handleAdoption, handleUnadoption}) {
    const { user } = useContext(UserContext)
    const [ shelterPets, setShelterPets ] = useState([])
    
    const poundPets = () => {
        fetch('api/shelter', {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => res.json())
        .then(data => setShelterPets(data))
    }

    useEffect(() => {
        poundPets()
    },[])

    return (<>
        <div className="card-container">
            <h1>Shelter</h1>
            {shelterPets.map(p => {return(
                <PetCard key={p.id} pet={p} pageName="shelter" isAdopted={false} />
            )})}
            <AddPet />
        </div>
    </>)
}