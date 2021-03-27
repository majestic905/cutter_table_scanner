import {useCallback, useState} from "react";
import Log from "./log";
import {Tab, Tabs, ImagesGrid} from './shared';


const Calibration = ({scan}) => {
    const [activeTab, setActiveTab] = useState('undistorted');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    const images = {};
    for (const name of ['original', 'undistorted']) {
        images[name] = {};
        for (const position of ['LU', 'LL', 'RU', 'RL']) {
            const src = scan.images[name][position].thumb;
            images[name][position] = {src, alt: src};
        }
    }
    for (const position of ['LU', 'LL', 'RU', 'RL'])
        images['undistorted'][position].url = scan.images['undistorted'][position].image;

    return (
        <div>
            <Tabs>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" isActive={activeTab === "undistorted"}/>
                <Tab onClick={selectTab} name="log" text="Log" isActive={activeTab === "log"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original}/>}
            {activeTab === "undistorted" && <ImagesGrid images={images.undistorted} isClickable/>}
            {activeTab === "log" && <Log text={scan.log}/>}
        </div>
    )
}


export default Calibration;