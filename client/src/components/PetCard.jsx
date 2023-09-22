import {useState, useEffect, useContext} from "react"
import { Card } from "react-bootstrap"

import { UserContext } from "../contexts/UserContext"
import "../styles/Card.css"
import defaultPet from "../assets/logos/defaultPet.png"

export default function PetCard({pet, pageName, isAdopted}) {
    const {user} = useContext(UserContext)
    const {name, strain, image="https://art.ngfiles.com/images/2961000/2961005_bezzathor_an-overly-simple-profile-picture-i-know-it-s-oversized.png?f1672592034"} = pet
    const {title, emoji} = strain
    const [page] = useState(pageName)
    const [adopted, setAdopted] = useState(isAdopted)
    const [error, setError] = useState(null)

    function handleAdoption() {
        fetch('/api/my_adoptions', {
            method: 'POST',
            headers: {'content-type': 'application/json'},
            body: JSON.stringify({
                pet_id: pet.id
            })
        })
        .then(res => res.json())
        .then(data => console.log(data))
        setAdopted(true)
    }
    
    function handleUnadoption() {
        fetch('/api/my_adoptions', {
            method: 'DELETE',
            headers: {'content-type': 'application/json'},
            body: JSON.stringify({
                pet_id: pet.id
            })
        })
        .then((res) => {
            if (res.status === 204) {
                setAdopted(false)
            } else if (res.status === 404) {
                setError("Not found")
            } else {
                setError(res.statusText)
            }
        }).then(data => console.log(data))
    }

    return (
    <div className="card-item">
        <div className="card-header">
            <h3>Name: <>{name}</></h3>
            <h4>Classification: <>{title} {emoji}</></h4>
        </div>
        <div className="card-display">
            <img src={image} alt="pet-photo" className="card-image"/>
        </div>
        <div className="card-actions">
            {page === "shelter" && user !== null
                ? !adopted 
                    ? <button onClick={ handleAdoption } className="btn">Adopt</button>
                    : <button onClick={ handleUnadoption } className="btn">Unadopt</button>
            :page === "mypets"
                ? <>
                    <button onClick={ ()=>{} } className="btn">Care</button>
                    <button onClick={ ()=>{} } className="btn">ViewDetails</button>
                    {adopted
                    ? <button onClick={ handleUnadoption } className="btn btn-danger"><small>unadopt</small></button>
                    : null}
                </> 
            :page === "ownerpets"
                ? <button onClick={ ()=>{} } className="btn">ViewDetails</button>
            : <p></p>
            }
        </div>
    </div>)
}