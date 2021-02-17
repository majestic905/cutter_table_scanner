import {useState, useCallback} from "react";
import cx from "classnames";


const ScanButton = ({onFinish}) => {
    const callApi = useCallback(() => {
        fetch('/api/scans', {method: 'POST'})
            .then(onFinish)
            .catch(error => console.error(error));
    }, [onFinish]);

    return (
        <button type="button" className='btn btn-sm bg-dark mr-2' onClick={callApi}>
            Полный скан
        </button>
    )
}


const CalibrateButton = ({onFinish}) => {
    const callApi = useCallback(() => {
        fetch('/api/cameras/projection_points/calibrate', {method: 'POST'})
            .then(onFinish)
            .catch(error => console.error(error));
    }, [onFinish]);

    return (
        <button type="button" className='btn btn-sm bg-dark mr-2' onClick={callApi}>
            Калибровка точек
        </button>
    )
}


const Image = ({selectedScan}) => {
    const imgSrc = `/api/scans/${selectedScan.name}`;
    // const imgUrl = `/api/scans/${selectedScan.name}?as_attachment=true`;
    const imgUrl = `${imgSrc}?as_attachment=true`;

    return (
        <div>
            <a href={imgUrl}>
                <img className="img-responsive"
                     src={imgSrc}
                     alt={selectedScan.name}
                />
            </a>
        </div>
    )
}

const Tab = ({text, active, name, onClick}) => {
    return (
        <li className={cx("tab-item", {active})} data-tab-name={name} onClick={onClick}>
            <a href="#">{text}</a>
        </li>
    )
}

const Tabs = ({activeTab, selectTab}) => {
    return (
        <ul className="tab tab-block">
            <Tab onClick={selectTab} name="original" text="Original" active={activeTab === "original"}/>
            <Tab onClick={selectTab} name="undistorted" text="Undistorted" active={activeTab === "undistorted"}/>
            <Tab onClick={selectTab} name="projected" text="Projected" active={activeTab === "projected"}/>
            <Tab onClick={selectTab} name="result" text="Result" active={activeTab === "result"}/>
        </ul>
    )
}


const Snapshot = ({loadScans, selectedScan}) => {
    const [activeTab, setActiveTab] = useState('original');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    return (
        <div id="scan-result">
            <header>
                <ScanButton onFinish={loadScans}/>
                <CalibrateButton onFinish={loadScans}/>
            </header>

            <hr/>

            <Tabs activeTab={activeTab} selectTab={selectTab} />

            {selectedScan
                ? <Image selectedScan={selectedScan}/>
                : <p className="text-italic">Выберите скан из списка</p>
            }
        </div>
    )
}

export default Snapshot;