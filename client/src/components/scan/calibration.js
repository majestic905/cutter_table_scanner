import {useCallback, useState} from "react";
import {Tab, Tabs, ImagesGrid} from './shared';


const Calibration = ({scan}) => {
    const [activeTab, setActiveTab] = useState('original');
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
            <Tabs activeTab={activeTab} selectTab={selectTab}>
                <Tab onClick={selectTab} name="original" text="Original" isActive={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" isActive={activeTab === "undistorted"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={images.original}/>}
            {activeTab === "undistorted" && <ImagesGrid images={images.undistorted} isClickable/>}
        </div>
    )
}


export default Calibration;