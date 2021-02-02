function Error({error}) {
    return (
        <div className="toast toast-error">
            <div>{JSON.stringify(error, null, 2)}</div>
        </div>
    )
}

export default Error;