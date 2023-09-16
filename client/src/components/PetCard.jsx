import { useState } from "react"
import { Card } from "react-bootstrap"
import Strain from "./Strain"

export default function PetCard({pet}) {
    const {name, factor, strain} = pet

    return (
    <div>
        <h3>{name}</h3>
        <Strain strain={strain}/>
    </div>)
}