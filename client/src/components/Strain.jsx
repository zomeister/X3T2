
export default function Strain ({strain}) {
    const {name, emoji} = strain
    return (<>
        {emoji}{name}{emoji}
    </>)
}