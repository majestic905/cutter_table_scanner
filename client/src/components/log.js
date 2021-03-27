const Log = ({text}) => {
    return (
        <textarea id="log" className="form-input" value={text} readOnly/>
    );
}

export default Log;