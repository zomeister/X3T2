import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import PetCard from "../PetCard"

export default function MyPets() {
    const { user } = useContext(UserContext)
    const [pets, setPets] = useState([])
    const myPets = () => {
        fetch(`/api/mypets`, {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => res.json())    
        .then(data => console.log(data))
        .catch(err => console.log(err))
    }
    useEffect(() => {
        myPets()
    }, [])

    return (<>
        MyPets
        {/* {pets.map(p => <PetCard key={p.id} pet={p} />)} */}
    </>)
}