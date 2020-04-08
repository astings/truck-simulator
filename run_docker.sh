if [ -z $1 ]
then 
    echo Running simulation with $1 trucks
    sudo NB_TRUCK=$1 docker-compose up
else
    echo Running simulation with 4 trucks by default
    sudo docker-compose up
fi