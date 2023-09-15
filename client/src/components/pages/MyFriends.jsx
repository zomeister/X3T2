import { useState, useContext, useEffect } from "react"
import { UserContext } from "../../contexts/UserContext"
import OwnerCard from "../OwnerCard"

export default function MyFriends() {
    const { user } = useContext(UserContext)
    const [username, setUsername] = useState(user.username)
    const [friends, setFriends] = useState([])
    const myFriends = () => {
        fetch(`${username}/friends`)
        .then(res => res.json())
        .then(data => setFriends(data))
        .catch(err => console.log(err))
    }
    
    useEffect(() => {
        myFriends()
    }, [])

    return (<>
        MyFriends
        {friends.map(o => <OwnerCard key={o.id} owner={o} />)}
    </>)
}