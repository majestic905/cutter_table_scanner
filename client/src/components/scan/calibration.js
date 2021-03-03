import {useCallback, useState} from "react";
import {Tab, Tabs, ImagesGrid} from './shared';


const Calibration = ({scan}) => {
    const [activeTab, setActiveTab] = useState('original');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    return (
        <div>
            <Tabs activeTab={activeTab} selectTab={selectTab}>
                <Tab onClick={selectTab} name="original" text="Original" active={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" active={activeTab === "undistorted"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={scan.images.ORIGINAL}/>}
            {activeTab === "undistorted" && <ImagesGrid images={scan.images.UNDISTORTED}/>}
        </div>
    )
}


export default Calibration;