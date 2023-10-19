<div align="center">
  <img src="https://github.com/h3nry-d1az/hngin/blob/main/assets/hngin-logo.png">
  <br>
  <br>
  <i>An attempt to implement a 3D rendering engine based on mere intuition and my little knowledge of linear algebra.</i>
</div>

<hr>

**ʜɴɢɪɴ** is an attempt to implement a three-dimensional rendering engine from scratch, based mainly on my intuition, my limited knowledge of linear algebra and some research and information gathering that I have carried out in order to achieve certain functionalities.

As can be inferred from the current state of the project, it should be treated for the moment as a proof of concept rather than a stable and secure product, since there are still many functionalities to be implemented that are necessary in any rendering engine (see the [to-do](https://github.com/h3nry-d1az/hngin#project-roadmap) section), as well as some possible bugs to cover, improve the code in many aspects and write documentation for all the features and operation of the software (however, for a greater understanding of this aspect one can go to the [intuition behind the engine](https://github.com/h3nry-d1az/hngin#intuition-behind-the-engine-code) section); it is also necessary to mention the detail that this program is written entirely in Python, which makes it relatively slow in comparison, although somewhat easier to read.

However, and as a result of the relatively important progress that I have been achieving in this project, I have decided to make it public and freely accessible in order to facilitate its use and to be able to receive suggestions, feedback and contributions from interested users.

## Run the demonstration program

<details open>
<summary>Section table of contents</summary>
<br>

1. [Clone the repository](https://github.com/h3nry-d1az/hngin#clone-the-repository)
2. [Getting the necessary dependencies.](https://github.com/h3nry-d1az/hngin#getting-the-necessary-dependencies)
3. [Running the engine source code.](https://github.com/h3nry-d1az/hngin#running-the-engine-source-code)
4. [Visual results of the program.](https://github.com/h3nry-d1az/hngin#visual-results-of-the-program)
5. [Packaging the program in an executable binary.](https://github.com/h3nry-d1az/hngin#packaging-the-program-in-an-executable-binary)

</details>

#### Clone the repository
First, one has to clone the code repository on its local machine using git, to do this, use the following command:
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


https://github.com/h3nry-d1az/hngin/assets/61124185/b1d58bfe-ab9c-4c51-890c-cdd01d74485a


#### Packaging the program in an executable binary
To compile the source code of the **ʜɴɢɪɴ** demo program to an executable binary, you will require the PyInstaller package on your machine, you can get it by running the following command:
```bash
pip install pyinstaller
```

Again, for more information you can go to the [project website](https://pyinstaller.org/). Once you have the dependencies installed on your device, proceed to execute the command shown below to produce the desired binary:
```bash
pyinstaller --onefile --noconsole ./main.py
```

The project binaries will **NOT** be available in the releases section.

## Project roadmap
Even though enough features have been implemented within the engine to have been able to make the decision to make it public, most of the functionalities that I would like to see covered and that I think would be feasible are not yet implemented. Therefore, below is the roadmap designed for the project (although without any date, it is more than likely that not all of them will end up being fulfilled):

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

1. [Introduction.](https://github.com/h3nry-d1az/hngin#introduction)
2. [Modeling the vertices of an object.](https://github.com/h3nry-d1az/hngin#modeling-the-vertices-of-an-object)
3. [Modeling faces as edges (vertex unions).](https://github.com/h3nry-d1az/hngin#modeling-faces-as-edges-vertex-unions)
4. [Projecting the vertices and edges.](https://github.com/h3nry-d1az/hngin#projecting-the-vertices-and-edges)
5. [A detail to keep in mind.](https://github.com/h3nry-d1az/hngin#a-detail-to-keep-in-mind)
6. [Camera rotations.](https://github.com/h3nry-d1az/hngin#camera-rotations)
7. [Works Cited.](https://github.com/h3nry-d1az/hngin#works-cited)

</details>

#### Introduction
The idea behind **ʜɴɢɪɴ** lies in, first, modeling three-dimensional objects through mathematical structures with which we can then operate (to, for example, move or rotate the said objects), and manipulate this three-dimensional space to project it into a two-dimensional one, since we can draw this on the screen easily using the pygame library mentioned above.

#### Modeling the vertices of an object
By its own definition, every vertex of a three-dimensional object consists of three coordinates: $x$, $y$ and $z$ [[1](), [2]()], thus we can model this vertex as a three-dimensional vector (of three components), linking this concept to the results of linear algebra and being able to operate with vertices of mathematical way. More rigorously, every vertex with coordinates $x$, $y$, $z$ corresponds to one and only one vector $\mathbf{p} = [x, y, z]$ such that $\mathbf{p} \in \mathbb{R}^3$.

#### Modeling faces as edges (vertex unions)
As mentioned in resources [[1](https://github.com/h3nry-d1az/hngin#works-cited)] and [[2](https://github.com/h3nry-d1az/hngin#works-cited)], three-dimensional objects (at least those in .obj format) are also composed of faces (triangles), however, we can simplify these as three edges that join three points, then our job is reduced to modeling these edges. Given $\mathbf{p}$ and $\mathbf{q}$ vertices, we will define an edge $\overline{\mathbf{p}\mathbf{q}}$ as the line segment that begins at $\mathbf{p}$ and ends at $\mathbf{q}$ [[6](https://github.com/h3nry-d1az/hngin#works-cited)], that is, that joins $\mathbf{p}$ with $\mathbf{q}$. Note that it is commutative, so $\overline{\mathbf{p}\mathbf{q}} = \overline{\mathbf{q}\mathbf{p}}$, since the said line segment is not oriented.

#### Projecting the vertices and edges
Once one has modeled the two fundamental concepts of three-dimensional objects (for the moment, since to date I do not know how to draw faces with solid colors nor work with normals) in a three-dimensional space, we will have to find a way to project it. so that we can see it on the screen, which is a two-dimensional surface.

###### Orthogonal projection
The first approach that one can take when facing this problem is to simply delete the $z$ coordinate of each three-dimensional vector and render the resulting two-dimensional vector, or what is equivalent and more formal taking into account the context of linear algebra, apply a linear transformation that simply "squishes space" onto a 2D surface, which corresponds to the following vector-by-matrix multiplication:

<div align="center">

  ![orthogonal](https://github.com/h3nry-d1az/hngin/assets/61124185/6e14e547-6b1b-4c55-902b-f4de7485aa39)

</div>

This procedure is called orthogonal projection [[3](https://github.com/h3nry-d1az/hngin#works-cited)], and although the intuition behind it is simple, the result, although clearly not perfect (I mean, the lack of depth and perspective is evident), is a valid starting point.

###### Projection based on focal length and linear interpolation
Another more accurate approach that we can take to this problem lies in the field of optics, and I must say that my knowledge in this branch of physics is constrained only to the limited research that I have done for the purpose of carrying out this project, so I quote verbatim the explanation behind the method I ended up using: "Let's assume you stand in front of a window, looking out. If you stand in the center of the window, looking out through the center of the window, then we can treat the center of your eye (more precisely, the center of the lens in the pupil of your dominant eye) the origin in 3D coordinates ... Let's say one of the 3D coordinates of an interesting detail, [any given point], are $(x,y,z)$. That ray intersects the window at $x'=x\cdot\frac{f}{z},y'=y\cdot\frac{f}{z},z'=f$. Therefore, the 2D coordinates of that detail on the window are: $(x' , y') = \left( x \frac{d}{z} , y \frac{d}{z} \right) = \frac{d}{z} ( x , y )$" [[4](https://github.com/h3nry-d1az/hngin#works-cited)]. In this case, as is obvious, the window is our screen.

To try to summarize and simplify this paragraph, we compare our screen with a window through which we see the scene, and through linear interpolation we can work and show that a point $(x,y,z)$ will have as coordinates in the window $(x\cdot\frac{f}{z},y\cdot\frac{f}{z},f)$, with $f$ being our focal length [[5](https://github.com/h3nry-d1az/hngin#works-cited)], then to project a vertex $\mathbf{p}$ we will have to apply the following transformation (note that it is not linear, we cannot use matrices in this case):

<div align="center">

![lerp](https://github.com/h3nry-d1az/hngin/assets/61124185/761d8e7b-57ff-42f4-b512-a95d8e1427da)

</div>

Since the window is our screen, we can delete the $z$ coordinate and render the resulting two-dimensional vector, we can use the previously seen orthographic projection for this:

<div align="center">

![orto-lerp](https://github.com/h3nry-d1az/hngin/assets/61124185/d8201250-ad97-46e2-bcdf-de496b175456)

</div>

And the resulting two-dimensional vector $\mathbf{p}'$ is the point to be rendered on the screen.

#### A detail to keep in mind
One must keep in mind that any point with a $z$ coordinate lower than that of the camera must not be rendered (nor the previous formulas applied), as it would cause graphic errors mainly when drawing the edges on the screen. I reiterate, with a $z$ coordinate less than that of the camera, that is, less than zero, since we are working with the camera being fixed at the origin; if it could be moved, you would simply have to subtract the vector in question and the vector with the camera position:
<div align="center">

![normalized-point](https://github.com/h3nry-d1az/hngin/assets/61124185/dde32f5e-66fc-4757-b40a-837bf184b119)

</div>

From this section on, when we refer to a vertex (vector) and its transformations, it must be normalized. Once the operations have been carried out, we can obtain the original vector again by adding the camera position vector to it:
<div align="center">

![original-point](https://github.com/h3nry-d1az/hngin/assets/61124185/c5c51ebd-777b-4057-928d-23c906493268)

</div>

#### Camera rotations
The most trivial (although valid, and the one I ended up using) approach one can take when implementing camera rotations in a three-dimensional space is to simply rotate the rest of the stage in the opposite direction, that is, rotate the camera to the left involves rotating the scene to the right, or rotating it up involves rotating it down.

This, however, raises two not so obvious questions: first, how to rotate a three-dimensional vector properly (as we will see later, in what order to apply the rotation matrices), and also, that the aforementioned 3D space consists of three axes, that is, six possible directions of rotation, while (ideally, and as it works in most systems) we only have four keys, two for vertical movement and another two for horizontal movement.

###### Rotate a three-dimensional vector
We will begin by resolving the first of the said questions. The space $\mathbb{R}^3$ has, as we have already mentioned, three coordinate axes: $X$, $Y$ and $Z$, therefore we can consider three different axes of rotation when rotating any vector $\mathbf{p}$, that is, there are three different rotation matrices we can employ in order to revolve our given $\mathbf{p}$ (one for each axis) [[7](https://github.com/h3nry-d1az/hngin#works-cited)]:

<div align="center">

![rotation_x](https://github.com/h3nry-d1az/hngin/assets/61124185/b3241dd0-6579-4701-8fb2-70a6a08d089b)

![rotation_y](https://github.com/h3nry-d1az/hngin/assets/61124185/8b5d0192-c5d2-411f-95d4-bf58e9c20815)

![rotation_z](https://github.com/h3nry-d1az/hngin/assets/61124185/82f2fa06-c758-4b46-8ec4-9a3098d83bcf)

</div>

As it is possible to infer, we need to rotate each vector around each of the three axes (with a rotation angle probably different for each of them), which implies applying each of these three matrices consecutively, or what is the same, apply the composition (product) of the three, that is, an even larger matrix.

<img align="left" src="https://github.com/h3nry-d1az/hngin/assets/61124185/f3ddfeee-928d-4d08-8af8-44c3097f9045" alt="the-world-if-meme" height="35%" width="35%"/>

The problem comes, however, that the product of these matrices is not commutative, that is, the order in which we apply these rotations matters, then rotate 27º around the $X$ axis, then 84º around the $Y$ and finally 11º around to $Z$, is not the same as 11º around $Z$, then 84º around $Y$ and finally 27º with respect to $X$. So, in what order should we apply these matrices? Most of the resources I consulted suggested applying $R_X$ first, then $R_Y$ and finally $R_Z$ [[7](https://github.com/h3nry-d1az/hngin#works-cited), [8](https://github.com/h3nry-d1az/hngin#works-cited), [10](https://github.com/h3nry-d1az/hngin#works-cited)] (I now understand that they were referring to another type of rotation, but not by then), except for one in particular that stated to first apply $R_Y$, then $R_X$ and finally $R_Z$ [[9](https://github.com/h3nry-d1az/hngin#works-cited)].

However, none of these methods worked, giving me wrong perspectives of the elements on the screen, which was because the rotation around the $Z$ axis was not working, looking like the example shown below:

https://github.com/h3nry-d1az/hngin/assets/61124185/f81e3a63-8dd9-439e-b34e-32544461e423

Thinking about it, if we first rotate around the $X$ and $Y$ axes, any element that is on the $X$ axis or, in general, in any position, and that we are looking at will be located right on the $Z$ axis, then applying a rotation around the $Z$ axis will make it rotate in the undesired way seen previously.

The solution? Get rid of the rotation around the $Z$ axis as soon as possible, that is, rotate about the aforementioned axis first, and then apply the rotation in $X$ and finally in $Y$. This method is the one that I ended up using and that, in truth, it works, getting results like the ones shown below:


https://github.com/h3nry-d1az/hngin/assets/61124185/357b3341-2b30-4e7c-a049-24f7601157f3


In general, for a vertex $\mathbf{p}$ and camera rotation angles $\theta_x$, $\theta_y$ and $\theta_z$, the three-dimensional vector resulting from the rotation process will be:

<div align="center">

![rotated](https://github.com/h3nry-d1az/hngin/assets/61124185/194d654e-d09d-4391-873a-4cda8f88e243)

</div>

Which, computed, has the following appearance:

<div align="center">

![rotation_computed](https://github.com/h3nry-d1az/hngin/assets/61124185/3c6ea1e8-ed05-4471-88c8-7c3540048b65)

</div>

And finally projected on screen:

<div align="center">

![rotated_and_projected](https://github.com/h3nry-d1az/hngin/assets/61124185/88c201f7-b09d-42b6-964a-678610e19173)

</div>

###### Camera rotation controls
Once we can rotate the camera properly, we have to simplify the necessary controls to only depend on four keys instead of six, that is, two that control the vertical rotation and two that control the horizontal one, instead of two for each axis.

The horizontal rotation is simple, because it remains the same as the rotation around the $Y$ axis, since it is independent of the others in the sense that, no matter the position of the camera, it will always work properly. We can assign two keys then to increment and decrement the $\theta_y$ angle.

Vertical rotation, however, is more complicated, since it is necessary to rotate around the $X$ and/or $Z$ axis, which depends on the value of $\theta_y$. When the camera is at the origin without having made any rotation, we are observing along the $Z$ axis, since this is the depth axis, while when we rotate our camera $\pm\frac{\pi}{2}$ radians, we are observing along the $X$ axis. That an element is located on the $Z$ axis requires a rotation around the $X$ axis so that the effect of verticality can be appreciated, since a rotation around $Z$ will produce the effect seen in the bad rotation example shown above, and vice versa happens with an element located in $X$, it will require a rotation around $Z$.

For now, we can create a special angle called $\lambda$ which stores the total vertical rotation, later we will convert it to $\theta_x$ and $\theta_z$. We will use two keys to increase and decrease the $\lambda$ value.

Now, when $\theta_y$ is 0 and we rotate vertically, we increment $\theta_x$ completely and do not touch $\theta_z$, while when $\theta_y$ takes the value of $\pm\frac{\pi}{2}$, $\theta_z$ increments completely and $\theta_x$ does not. For any angle $\theta_y$, we can then generalize and define $\theta_x$ and $\theta_z$ in terms of $\theta_y$ and $\lambda$ using trigonometry:

<div align="center">

![thetax_thetaz_lambda](https://github.com/h3nry-d1az/hngin/assets/61124185/971c4c61-1205-4433-b035-391ed0035d32)

</div>

Finally, to avoid graphical errors, we will keep the $\theta_x$, $\theta_y$ and $\theta_z$ angles ($\theta_y$ and $\lambda$) always in the interval $[-\pi, \pi]$.

#### Works Cited
1. *Guidance to write a parser for .Obj and mtl file*, http://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm. Accessed 3 October 2023.
2. *CS 418 - Parsing OBJ Files*, 17 April 2023, https://cs418.cs.illinois.edu/website/text/obj.html. Accessed 3 October 2023.
3. Margalit, Dan, and Joseph Rabinoff. *Orthogonal Projection*, https://textbooks.math.gatech.edu/ila/projections.html. Accessed 4 October 2023.
4. “3D projection on a 2D plane ( weak maths ressources ).” *Mathematics Stack Exchange*, 1 June 2017, https://math.stackexchange.com/questions/2305792/3d-projection-on-a-2d-plane-weak-maths-ressources. Accessed 4 October 2023.
5. “Focal Length of a Lens.” *HyperPhysics Concepts*, http://hyperphysics.phy-astr.gsu.edu/hbase/geoopt/foclen.html. Accessed 4 October 2023.
6. *Euclid's Postulates*, https://people.math.harvard.edu/~ctm/home/text/class/harvard/113/97/html/euclid.html. Accessed 4 October 2023.
7. *3DRotations*, http://motion.pratt.duke.edu/RoboticSystems/3DRotations.html. Accessed 6 October 2023.
8. “Rotation matrix.” *Wikipedia*, https://en.wikipedia.org/wiki/Rotation_matrix. Accessed 6 October 2023.
9. “How to Make a Three-Dimensional Project.” *Scratch Wiki*, 2 July 2023, https://en.scratch-wiki.info/wiki/How_to_Make_a_Three-Dimensional_Project#Rotation. Accessed 6 October 2023.
10. Plein, Dominic. “Extrinsic & intrinsic rotation: Do I multiply from right or left?” Dominic Plein, 2 May 2022, https://dominicplein.medium.com/extrinsic-intrinsic-rotation-do-i-multiply-from-right-or-left-357c38c1abfd. Accessed 6 October 2023.

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
