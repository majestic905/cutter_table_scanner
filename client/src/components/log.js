const Log = ({text}) => {
    return (
        <div className="container grid-lg">
            <textarea id="log" className="form-input" value={text} readOnly/>
        </div>
    );
}

export default Log;