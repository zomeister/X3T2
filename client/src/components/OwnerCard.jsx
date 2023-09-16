import {useState} from "react"
import { Card } from "react-bootstrap"

export default function OwnerCard({owner}) {
    const {first_name, last_name, profile_url, city, bio} = owner
    return (<div>
        {first_name} {last_name}
    </div>)
}