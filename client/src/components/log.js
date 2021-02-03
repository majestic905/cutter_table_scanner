const LogItem = ({timestamp, message}) => {
    return (
        <li>
            <span className="log-timestamp text-gray">[{timestamp.toLocaleTimeString()}]</span>
            {' '}
            <span className="log-message">{message}</span>
        </li>
    );
};


const Log = ({logItems}) => {
    return (
        <div className="no-scrollbar" id="column-log">
            <h5>Лог</h5>
            <ul className="text-small">
                {logItems.map(item => <LogItem key={item.id} timestamp={item.timestamp} message={item.message} />)}
            </ul>
        </div>
    );
}

export default Log;