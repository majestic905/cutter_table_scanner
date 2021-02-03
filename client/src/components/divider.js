const Divider = ({vertical}) => {
    const className = vertical ? "divider-vert" : "divider";

    return (
        <div className={className}/>
    );
};

export default Divider;