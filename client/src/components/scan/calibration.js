import {useCallback, useState, useEffect} from "react";
import {Tab, Tabs, ImagesGrid} from './shared';


const Input = ({label, name, placeholder, onChange, value}) => {
    return (
        <div className="form-group">
            <div className="col-3 col-sm-12">
                <label className="form-label label-sm">{label}</label>
            </div>
            <div className="col-9 col-sm-12">
                <input className="form-input input-sm" type="text" name={name} value={value} onChange={onChange}
                       placeholder={placeholder}
                />
            </div>
        </div>
    )
}

const PointInput = ({label, name, onChange, point}) => {
    return (
        <div className="column col-6 d-flex">
            <label className="form-label label-sm mr-2">{label}:</label>
            <input className="form-input input-sm mr-2" type="number" value={point.x} name={`${name}.x`} onChange={onChange}/>
            <input className="form-input input-sm" type="number" value={point.y} name={`${name}.y`} onChange={onChange}/>
        </div>
    )
}


const CameraFields = ({title, cameraPosition, onChange, data}) => {
    return (
        <fieldset className="my-0">
            <legend className="my-0">{title}</legend>
            <div className="form-horizontal">
                <Input label="Name" name={`${cameraPosition}.maker`}
                       value={data.maker} onChange={onChange} placeholder="Canon" />
                <Input label="Model" name={`${cameraPosition}.model`}
                       value={data.model} onChange={onChange} placeholder="Canon Powershot S50" />
                <Input label="USB Port" name={`${cameraPosition}.usb_port`}
                       value={data.usb_port} onChange={onChange} placeholder="/dev/usb1" />
            </div>
            <div>
                <label className="form-label label-sm">Projection points:</label>
                <div className="columns">
                    <PointInput label="LU" name={`${cameraPosition}.projection_points.LU`}
                                point={data.projection_points.LU} onChange={onChange} />
                    <PointInput label="RU" name={`${cameraPosition}.projection_points.RU`}
                                point={data.projection_points.RU} onChange={onChange} />
                    <PointInput label="LL" name={`${cameraPosition}.projection_points.LL`}
                                point={data.projection_points.LL} onChange={onChange} />
                    <PointInput label="RL" name={`${cameraPosition}.projection_points.RL`}
                                point={data.projection_points.RL} onChange={onChange} />
                </div>
            </div>
        </fieldset>
    )
}


const SubmitSection = ({data}) => {
    const [message, setMessage] = useState();

    const doSubmit = (ev) => {
        ev.preventDefault();
        setMessage(undefined);

        fetch('/api/cameras', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
            .then(response => setMessage(`Status: ${response.status} ${response.statusText}`))
            .catch(error => setMessage(error.message));
    }

    return (
        <div className="column col-12">
            {message && <div className="toast toast-primary mb-2">{message}</div>}
            <input type="submit" className="btn btn-primary" value="Отправить" onClick={doSubmit}/>
        </div>
    )
}


const CamerasForm = () => {
    const [data, setData] = useState();

    const onPointChange = useCallback(ev => {
        const [cameraPosition,, pointPosition, dimension] = ev.target.name.split('.');
        const value = parseFloat(ev.target.value);

        setData(data => ({
            ...data,
            [cameraPosition]: {
                ...data[cameraPosition],
                projection_points: {
                    ...data[cameraPosition].projection_points,
                    [pointPosition]: {
                        ...data[cameraPosition].projection_points[pointPosition],
                        [dimension]: value
                    }
                }
            }
        }));
    }, [setData]);

    const onChange = useCallback(ev => {
        const [cameraPosition, field] = ev.target.name.split('.');

        if (field === "projection_points")
            return onPointChange(ev);

        setData(data => ({
            ...data,
            [cameraPosition]: {
                ...data[cameraPosition],
                [field]: ev.target.value
            }
        }));
    },[setData, onPointChange]);

    useEffect(() => {
        fetch('/api/cameras')
            .then(res => res.json())
            .then(data => setData(data))
            .catch(error => console.error(error));
    }, []);

    if (!data)
        return <div>Loading...</div>;

    return (
        <form className="columns">
            <div className="column">
                <CameraFields title="Камера LU" cameraPosition="LU" data={data.LU} onChange={onChange}/>
                <hr/>
                <CameraFields title="Камера LL" cameraPosition="LL" data={data.LL} onChange={onChange}/>
            </div>

            <div className="divider-vert"/>

            <div className="column">
                <CameraFields title="Камера RU" cameraPosition="RU" data={data.RU} onChange={onChange}/>
                <hr/>
                <CameraFields title="Камера RL" cameraPosition="RL" data={data.RL} onChange={onChange}/>
            </div>

            <SubmitSection data={data}/>
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