import logo from "../logo.svg";

function Images() {
    return (
        <div className="column no-scrollbar" id="column-images">
            <h5>Изображения</h5>

            <div className="columns" id="container-images">
                <div className="column col-6">
                    <figure className="figure">
                        <img className="img-responsive" src={logo} alt="Image #1"/>
                        <figcaption className="figure-caption text-center">Image #1</figcaption>
                    </figure>
                </div>
                <div className="column col-6">
                    <figure className="figure">
                        <img className="img-responsive" src={logo} alt="Image #2"/>
                        <figcaption className="figure-caption text-center">Image #2</figcaption>
                    </figure>
                </div>
                <div className="column col-6">
                    <figure className="figure">
                        <img className="img-responsive" src={logo} alt="Image #3"/>
                        <figcaption className="figure-caption text-center">Image #3</figcaption>
                    </figure>
                </div>
                <div className="column col-6">
                    <figure className="figure">
                        <img className="img-responsive" src={logo} alt="Image #4"/>
                        <figcaption className="figure-caption text-center">Image #4</figcaption>
                    </figure>
                </div>
            </div>

            <hr/>

            <figure className="figure">
                <img className="img-responsive" src='/logo512.png' alt="Image #4"/>
                <figcaption className="figure-caption text-center">
                    Resulting image
                </figcaption>
            </figure>
        </div>
    )
}

export default Images;