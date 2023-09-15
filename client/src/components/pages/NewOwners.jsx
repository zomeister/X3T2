import { useState, useContext, useEffect } from "react"
import OwnerCard from "../OwnerCard"

export default function NewOwners() {
    const [newOwners, setNewOwners ] = useState([])
    
    const getOwners = () => {
        fetch('api/owners', {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => res.json())
        .then(data => setNewOwners(data))
    }

    useEffect(() => {
        getOwners()
    },[])

    return (<>
        {newOwners.map(o => <OwnerCard key={o.id} owner={o}/>)}
    </>)
}