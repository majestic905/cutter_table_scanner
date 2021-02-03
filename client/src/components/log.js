const LogItem = ({timestamp, message}) => {
    return (
        <li>
            <span className="log-timestamp text-gray">[{timestamp.toLocaleTimeString()}]</span>
            <span className="log-message">{message}</span>
        </li>
    );
};


const Log = ({size, logItems}) => {
    return (
        <div className={`column col-${size} no-scrollbar`} id="column-log">
            <h5>Лог</h5>

            <ul className="text-small">
                {logItems.map(item => <LogItem timestamp={item.timestamp} message={item.message} />)}
            </ul>
        </div>
    );
}

export default Log;