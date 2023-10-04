<div align="center">
  <img src="https://github.com/h3nry-d1az/hngin/blob/main/assets/hngin-logo.png">
  <br>
  <br>
  <i>An attempt to implement a 3D rendering engine based on mere intuition and my little knowledge of linear algebra.</i>
</div>

<hr>

**ʜɴɢɪɴ** is an attempt to implement a three-dimensional rendering engine from scratch, based mainly on my intuition, my limited knowledge of linear algebra and some research and information gathering that I have carried out in order to achieve certain functionalities.

As can be inferred from the current state of the project, it should be treated for the moment as a proof of concept rather than a stable and secure product, since there are still many functionalities to be implemented that are necessary in any rendering engine (see the [to-do]() section), as well as some possible bugs to cover, improve the code in many aspects and write documentation for all the features and operation of the software (however, for a greater understanding of this aspect one can go to the [intuition behind the engine]() section); It is also necessary to mention the detail that this program is written entirely in Python, which makes it relatively slow in comparison, although somewhat easier to read.

However, and as a result of the relatively important progress that I have been achieving in this project, I have decided to make it public and freely accessible in order to facilitate its use and to be able to receive suggestions, feedback and contributions from interested users.

## Run the demonstration program

<details open>
<summary>Section table of contents</summary>
<br>

1. [Clone the repository]()
2. [Getting the necessary dependencies.]()
3. [Running the engine source code.]()
4. [Visual results of the program.]()

</details>

#### Clone the repository
First, one has to clone the code repository on your local machine using git, to do this, use the following command:
```bash
git clone https://github.com/h3nry-d1az/hngin.git
```
Once the repository is cloned, proceed to move to the recently cloned directory using the command shown below:
```bash
cd hngin/
```

#### Getting the necessary dependencies
In order to run the demo program, you must have the pygame library installed, which is responsible for managing two-dimensional graphics. If you do not have the aforementioned module installed on your system, you can obtain it with the following command:
```bash
pip install pygame
```
For more information, one can go to the [official website](https://www.pygame.org/) of the said library.

#### Running the engine source code
Once the previous dependencies have been installed, one can finally run the engine demo program. To do this, first go to the root directory of this project and run the following command in your terminal:
```bash
python ./main.py
```

Which should cause two windows to be displayed on the screen, a rectangular one (640x480), centered on the screen (approximately) and a longer one located right next to it, which processes the engine configurations.

#### Visual results of the program
The aforementioned windows should look as shown below:

<video> 
  <source src="" type="video/mp4"> 
</video>

## Project roadmap
Even though enough features have been implemented within the engine to have been able to make the decision to make it public, most of the functionalities that I would like to see implemented and that I think would be feasible are not yet implemented. Therefore, below is the roadmap designed for the project (although without any date, it is more than likely that not all of them will end up being fulfilled):

- [X] [Achieve orthogonal projection.](https://github.com/h3nry-d1az/hngin/tree/91eef2ba994b3fea536ff25a397b62b72d9e82e5)
- [X] [Achieve projection based on focal length and linear interpolation.](https://github.com/h3nry-d1az/hngin/tree/c9613bdb4194ea96fc4b72bbc003aec0d7145aaa)
- [X] [Importing .obj files (vertices).](https://github.com/h3nry-d1az/hngin/tree/d827c81ccd1772b8cd1bf25c3a9eb9ef99e844fb)
- [X] [Importing .obj files (faces).](https://github.com/h3nry-d1az/hngin/tree/38ef1b6ac8f221972e7d57ccf336842483cb921a)
- [X] [Fix visual glitches.](https://github.com/h3nry-d1az/hngin/tree/88b99ed805da7fda49897e1473ff67d2724ebebe)
- [X] [Implement camera rotations.](https://github.com/h3nry-d1az/hngin/tree/3233cb4fdd171ce86cddf49c5fb0a89e19567097)
- [X] [Implement a settings bar.](https://github.com/h3nry-d1az/hngin/tree/6ef936bac3ce936e5f04910698c3af268673e1d4)
- [ ] Change the use of edges for faces.
- [ ] Optimize code and improve execution speed.
- [ ] Add solid colors to the models' faces.
- [ ] Add support for textures in models.

(Almost) all progress on this project has been recorded and saved to the YouTube playlist ["Motor 3D ʜɴɢɪɴ"](https://youtube.com/playlist?list=PLwG1fQu9A7F3SG0JXcnpE5Zx_uLFYuLz9&si=w7sWMobJYwKLGsbH). Any contribution that helps carry out the above goals will always be welcome.

## Intuition behind the engine code

<details open>
<summary>Section table of contents</summary>
<br>

1. []()

</details>

## [License](https://github.com/h3nry-d1az/hngin/blob/main/LICENSE)
MIT License

Copyright (c) 2023 Henry Díaz Bordón

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<br>
<br>

> This project is dedicated mainly to my **parents**, who, despite being very far away, are still with me; but also to my **host family**, to whom I couldn't be more grateful for all the effort they are making.
