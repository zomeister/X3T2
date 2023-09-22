import {useState, useEffect, useContext} from "react"
import { Card } from "react-bootstrap"
import defaultPet from "../assets/logos/defaultPet.png"
import "../styles/Card.css"

export default function OwnerCard({owner, pageName}) {
    const {bio, city, first_name, last_name, profile_url} = owner
    const [page] = useState(pageName)

    return (
    <div className="card-item">
        <div className="card-header">
            <h3>Name: {first_name} {last_name}</h3>
            <h4>City: {city}</h4>
        </div>
        <div className="card-display">
            <img src={profile_url} alt={first_name} className="card-image"/>
        </div>
        <div className="card-actions">
            {bio}
        </div>
    </div>)
}