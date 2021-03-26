
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file depression.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The depression header file
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#ifndef HEXAGONHYDRO_DEPRESSION_H
#define HEXAGONHYDRO_DEPRESSION_H

#include <vector>

#include "hexagon.h"
namespace hexwatershed
{

class depression
{
    std::vector<hexagon> find_the_boundary(std::vector<hexagon> cCell);

    int depression_fill(std::vector<hexagon> cCell);
};
} // namespace hexwatershed

#endif //HEXAGONHYDRO_DEPRESSION_H
