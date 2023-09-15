import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import PetCard from "../PetCard"

export default function MyPets() {
    const { user } = useContext(UserContext)
    const [username, setUsername] = useState(user.username)
    const [pets, setPets] = useState([])
    const myPets = () => {
        fetch(`${username}/pets`)
        .then(res => res.json())
        .then(data => setPets(data))
        .catch(err => console.log(err))
    }
    
    useEffect(() => {
        myPets()
    }, [])

    return (<>
        MyPets
        {pets.map(p => <PetCard key={p.id} pet={p} />)}
    </>)
}