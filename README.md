# Gungnir
Gungnir is a tool to download and analyze free XR applications from SideQuest Marketplace, developed by Anfonso R. Barredo-Valenzuela while at IMDEA Networks. It is composed by two functionalities. First, a crawler used for searching and gathering APKs. Second, a script to extract relevant information from the extracted dataset.


## Requirements 
The use of this software requires having several items before.
- HARDWARE
    - Meta Headset (e.g., Meta Quest 3) in Developer mode.
- SOFTWARE
    - **SideQuest Desktop** app installed on the PC.
        - User account credentials must be provided and filled in at `./crawler/configuration.py`. 
    - **Google Chrome** installed (if you want you can change the selenium driver for using another browser).
    - **Il2CppDumper**
    - **Jadx**
    - (Optional) Having installed the Meta Developer Hub.

For the Python scripts, run this command for installing dependencies: 

```bash
pip install -r requirements.txt 
```

## Usage

Any of them require further inputs than the those in the configuration files.

## Results

The APKs gathered by the crawler are stored in `./Data/APKs`. The results of the analysis are in the folder `./graphs/freq`.


## Our Work

Use the following citation to acknowledge our work:

Barredo-Valenzuela, A. R., Portillo, S. P., Vallina-Rodriguez, N., & Suarez-Tangil, G. (2024, August). Reversing the Virtual Maze: An Overview of the Technical and Methodological Challenges for Metaverse App Analysis. In 2024 IEEE International Conference on Metaverse Computing, Networking, and Applications (MetaCom) (pp. 173-181). IEEE.

```
@inproceedings{barredo2024reversing,
  title={Reversing the Virtual Maze: An Overview of the Technical and Methodological Challenges for Metaverse App Analysis},
  author={Barredo-Valenzuela, Alfonso Rodriguez and Portillo, Sergio Pastrana and Vallina-Rodriguez, Narseo and Suarez-Tangil, Guillermo},
  booktitle={2024 IEEE International Conference on Metaverse Computing, Networking, and Applications (MetaCom)},
  pages={173--181},
  year={2024},
  organization={IEEE}
}
```

## Acknowledgements

Part of this research was supported by the Spanish National Cybersecurity Institute (INCIBE) under Proyectos Estratégicos de Ciberseguridad -- CIBERSEGURIDAD EINA UNIZAR and by the Recovery, Transformation and Resilience Plan funds, financed by the European Union (Next Generation).

![INCIBE_logos](INCIBE_logos.jpg)
