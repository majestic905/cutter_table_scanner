import {useCallback, useState} from "react";
import {Tab, Tabs, ImagesGrid} from './shared';


const Input1 = ({label, name, placeholder}) => {
    return (
        <div className="form-group">
            <div className="col-3 col-sm-12">
                <label className="form-label label-sm">{label}</label>
            </div>
            <div className="col-9 col-sm-12">
                <input className="form-input input-sm" type="text" name={name} placeholder={placeholder}/>
            </div>
        </div>
    )
}

const Input2 = ({label, name}) => {
    return (
        <div className="column col-6 d-flex">
            <label className="form-label label-sm mr-2">{label}:</label>
            <input className="form-input input-sm" type="text" name={name}/>
        </div>
    )
}


const CameraFields = ({title, cameraPosition}) => {
    return (
        <fieldset className="my-0">
            <legend className="my-0">{title}</legend>
            <div className="form-horizontal">
                <Input1 label="Name" name={`${cameraPosition}.maker`} placeholder="Canon"/>
                <Input1 label="Model" name={`${cameraPosition}.model`} placeholder="Canon Powershot S50"/>
                <Input1 label="USB Port" name={`${cameraPosition}.usb_port`} placeholder="/dev/usb1"/>
            </div>
            <div>
                <label className="form-label label-sm">Projection points</label>
                <div className="columns">
                    <Input2 label="LU" name={`${cameraPosition}.projection_points.LU`} />
                    <Input2 label="RU" name={`${cameraPosition}.projection_points.RU`} />
                    <Input2 label="LL" name={`${cameraPosition}.projection_points.LL`} />
                    <Input2 label="RL" name={`${cameraPosition}.projection_points.RL`} />
                </div>
            </div>
        </fieldset>
    )
}


const CamerasForm = () => {
    return (
        <form className="columns">
            <div className="column">
                <CameraFields title="Камера LU" cameraPosition="LU"/>
                <hr/>
                <CameraFields title="Камера LL" cameraPosition="LL"/>
            </div>

            <div className="divider-vert"/>

            <div className="column">
                <CameraFields title="Камера RU" cameraPosition="RU"/>
                <hr/>
                <CameraFields title="Камера RL" cameraPosition="RL"/>
            </div>

            <div className="column col-12">
                <input type="submit" className="btn btn-primary" value="Отправить"/>
            </div>
        </form>
    )
};


const Calibration = ({scan}) => {
    const [activeTab, setActiveTab] = useState('original');
    const selectTab = useCallback(ev => setActiveTab(ev.currentTarget.dataset.tabName), [setActiveTab]);

    return (
        <div>
            <Tabs activeTab={activeTab} selectTab={selectTab}>
                <Tab onClick={selectTab} name="original" text="Original" active={activeTab === "original"}/>
                <Tab onClick={selectTab} name="undistorted" text="Undistorted" active={activeTab === "undistorted"}/>
                <Tab onClick={selectTab} name="form" text="Form" active={activeTab === "form"}/>
            </Tabs>

            {activeTab === "original" && <ImagesGrid images={scan.images.ORIGINAL}/>}
            {activeTab === "undistorted" && <ImagesGrid images={scan.images.UNDISTORTED}/>}
            {activeTab === "form" && <CamerasForm />}
        </div>
    )
}


export default Calibration;