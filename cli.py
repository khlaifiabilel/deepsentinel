import click, os, logging
from datetime import datetime as dt
from click import command, option, Option, UsageError

logging.basicConfig(level=logging.INFO)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--conf', default=os.path.join(os.getcwd(),'conf','DATA_CONFIG.yaml'), help='path to DATA_CONFIG.yaml')
@click.option('--n-orbits', help='The number of orbits to spread the simulated points over.', type=int) # one of N_orbits, end_date, pts per orbit
@click.option('--end-date', help='the end date to stop sampling points, as YYYY-mm-dd', type=str)
@click.option('--iso2', help='A comma-separated list of iso-a2 country codes for geographic subsampling', type=str)
@click.argument('start_date', type=str)
@click.argument('n-points', type=int)
@click.argument('name', type=str)
def generate_points(name, n_points, start_date, iso2, end_date, n_orbits, conf):
    """
    A method to seed points for a new dataset.
    
    \b
    PARAMETERS
    ----------
    NAME: str
        The name of the new dataset.
        
    N_POINTS: int
        The number of data points to generate.
        
    START_DATE: str
        The start date for data collection in the form YYYY-mm-dd.
    """
    
    from deepsentinel.utils.point_generator import PointGenerator
    logger = logging.getLogger('GENERATE_POINTS')

    
    # error check either end_date OR n_orbits
    assert (end_date or n_orbits), 'Only one of n_orbits or end_date must be provided.'
    assert not (end_date and n_orbits), 'Only one of n_orbits or end_date must be provided.'
    
    # error check date formats
    try:
        start_date = dt.strptime(start_date,'%Y-%m-%d')
    except:
        raise ValueError('Ensure start_date is in the correct format, YYYY-mm-dd')
    if end_date!=None:
        try:
            end_date = df.strptime(end_date,'%Y-%m-%d')
        except:
            raise ValueError('Ensure end_date is in the correct format, YYYY-mm-dd')
                   
    logger.info('Generating points with:')
    logger.info(f'NAME:{name}')
    logger.info(f'N_POINTS:{n_points}')
    logger.info(f'START_DATE:{start_date}')
    logger.info(f'iso2:{iso2}')
    logger.info(f'end_date:{end_date}')
    logger.info(f'n_orbits:{n_orbits}')
    logger.info(f'conf:{conf}')
    
    if iso2:
        iso2 = iso2.split(',')
    
    logger.info('Initialising generator')
    generator=PointGenerator(iso_geographies=iso2, conf=conf)
    
    if not n_orbits: # get n_orbits from end_date
        n_orbits = (end_date-start_date).days // generator.CONFIG['orbit_period']
        pts_per_orbit = n_points//n_orbits + 1
    else: # have n_orbits, get pts_per_orbit
        pts_per_orbit = n_points//n_orbits + 1
        
    logger.info(f'Running generator for {name} from {start_date.isoformat()} for {n_orbits} orbits with {pts_per_orbit} points per orbit')
    generator.main_generator(start_date, n_orbits, pts_per_orbit,name)

@cli.command()
def generate_samples():
    # TODO
    pass

    
@cli.command()
def train():
    from deepsentinel.main import ex

    r = ex.run()



if __name__=="__main__":
    cli()

