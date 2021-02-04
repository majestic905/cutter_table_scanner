const LogItem = ({timestamp, message}) => {
    return (
        <li>
            <span className="log-timestamp text-gray">[{timestamp.toLocaleTimeString()}]</span>
            {' '}
            <span className="log-message">{message}</span>
        </li>
    );
};


const ClearButton = ({doClear}) => {
    return (
        <span className='header-button' onClick={doClear}>
            Очистить
        </span>
    )
}


const Log = ({logItems, clearLog}) => {
    return (
        <div id="log">
            <header>
                <h5 className="d-inline">Лог</h5>
                <ClearButton doClear={clearLog} />
            </header>

            <ul className="text-small">
                {logItems.map(item => <LogItem key={item.id} timestamp={item.timestamp} message={item.message} />)}
            </ul>
        </div>
    );
}

export default Log;