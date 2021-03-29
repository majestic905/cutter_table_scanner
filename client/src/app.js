import {useState, useEffect} from "react";
import useFetch from "./hooks/useFetch";
import Header from "./components/header";
import Snapshot from "./components/snapshot";
import Calibration from "./components/calibration";
import './app.scss';


function App() {
    const [scan, setScan] = useState(null);

    const [{isLoading, response, error}, getScan] = useFetch("/api/scan");

    useEffect(getScan, [getScan]);

    useEffect(() => {
        if (response)
            setScan(response);
        else if (error)
            alert(`Ошибка при загрузке скана: ${error}`);
    }, [response, error]);

    return (
        <main>
            <Header getScan={getScan} />

            {isLoading && <div className="loading mt-2"/>}
            {scan?.scanType === "snapshot" && <Snapshot scan={scan}/>}
            {scan?.scanType === "calibration" && <Calibration scan={scan}/>}
        </main>
    );
}

export default App;
