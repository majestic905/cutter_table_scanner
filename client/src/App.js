import {useState, useEffect, useCallback} from "react";

import ScansList from "./components/scans_list";
import Images from "./components/images";
import Log from "./components/log";
import Divider from "./components/divider";

import './App.scss';



function App() {
    const [logItems, setLogItems] = useState([]);

    const addLogItem = useCallback((message) => {
        setLogItems(items => {
            const item = {id: items.length + 1, timestamp: new Date(), message};
            return [item, ...items];
        });
    }, [setLogItems]);

    useEffect(() => { for (let i = 0; i < 30; ++i) addLogItem("App initialized"); }, []);

    // ------------

    const [scans, setScans] = useState(null);
    const [selectedScan, setSelectedScan] = useState(null);

    const loadScans = useCallback(() => {
        setSelectedScan(null);

        fetch('/api/scans')
            .then(res => res.json())
            .then(data => setScans(data.scans))
            .catch(error => console.error(error));
    }, [setScans, setSelectedScan]);

    useEffect(loadScans, []);

    // ------------


    return (
        <main className="container 100vh">
            <div className="columns 100vh">
                <ScansList scans={scans} loadScans={loadScans}
                           selectedScan={selectedScan} selectScan={setSelectedScan}
                />

                <Divider vertical />

                <div className="column 100vh" id="column-right">
                    <Images loadScans={loadScans} />

                    <Divider />

                    <Log logItems={logItems}/>
                </div>
            </div>
        </main>
    );
}

export default App;
