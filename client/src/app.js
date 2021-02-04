import {useState, useEffect, useCallback} from "react";

import ScansList from "./components/scans_list";
import ScanResult from "./components/scan_result";
import Log from "./components/log";
import Divider from "./components/divider";

import './app.scss';



function App() {
    const [logItems, setLogItems] = useState([]);

    const addLogItem = useCallback((message) => {
        setLogItems(items => {
            const item = {id: items.length + 1, timestamp: new Date(), message};
            return [item, ...items];
        });
    }, [setLogItems]);

    const clearLog = useCallback(() => { setLogItems([]) }, []);

    useEffect(() => { for (let i = 0; i < 10; ++i) addLogItem("App initialized"); }, []);

    // ------------

    const [scans, setScans] = useState(null);
    const [selectedScan, setSelectedScan] = useState(null);

    const loadScans = useCallback(() => {
        setSelectedScan(null);

        fetch('/api/scans')
            .then(res => res.json())
            .then(data => {
                setScans(data.scans);
                if (data.scans.length > 0)
                    setSelectedScan(data.scans[0]);
            })
            .catch(error => console.error(error));
    }, [setScans, setSelectedScan]);

    useEffect(loadScans, []);

    // ------------

    console.log(scans);

    return (
        <main className="container">
            <div className="columns">
                <div className="column col-3" id="column-left">
                    <ScansList scans={scans} loadScans={loadScans}
                           selectedScan={selectedScan} selectScan={setSelectedScan}
                    />

                    <Divider />

                    <Log logItems={logItems} clearLog={clearLog}/>
                </div>

                <Divider vertical />

                <div className="column" id="column-right">
                    <ScanResult loadScans={loadScans} selectedScan={selectedScan} />
                </div>
            </div>
        </main>
    );
}

export default App;
