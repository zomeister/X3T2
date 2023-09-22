import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import PetCard from "../PetCard"

export default function MyPets({handleAdoption, handleUnadoption}) {
    const { user } = useContext(UserContext)
    // const [username, setUsername] = useState(user.username)
    const [pets, setPets] = useState([])
    function myPets () {
        fetch(`/api/mypets`, {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => res.json())
        .then(data => setPets(data))
        .catch(err => console.log(err))
    }

    useEffect(() => {
        myPets()
    }, [])

    return (<>
        <h1>My Pets</h1>
        {pets.map(p => <PetCard key={p.id} pet={p} pageName="mypets" isAdopted={true} />)}
    </>)
}