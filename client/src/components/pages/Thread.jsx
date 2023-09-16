import { useContext, useState, useEffect } from "react"

import { UserContext } from "../../contexts/UserContext"
import MessageCard from "../MessageCard"

export default function Thread ({username}) {
    const { user } = useContext(UserContext)
    return (
        <div>
            Messages
        </div>
    )
}