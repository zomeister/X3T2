
export default function Strain ({strainInfo}) {
    const {name, emoji} = strainInfo
    return (<>
        <section>{emoji} {name} {emoji}</section>
    </>)
}