
export default function PetDetail ({stat}) {
    const {happiness, health, hunger, pet_id} = stat
    return (
    <>
        <p>Happiness: {happiness}</p>
        <p>Health: {health}</p>
        <p>Hunger: {hunger}</p>
    </>
)}