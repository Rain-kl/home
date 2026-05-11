/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package net.arctel.cms.service.impl;

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import java.util.ArrayList;
import java.util.List;
import net.arctel.cms.entity.CmsSiteLink;
import net.arctel.cms.input.SiteLinkInput;
import net.arctel.cms.mapper.CmsSiteLinkMapper;
import net.arctel.cms.service.CmsSiteLinkService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CmsSiteLinkServiceImpl extends ServiceImpl<CmsSiteLinkMapper, CmsSiteLink>
        implements CmsSiteLinkService {

    @Override
    public List<CmsSiteLink> listEnabled() {
        return list(new LambdaQueryWrapper<CmsSiteLink>()
                .eq(CmsSiteLink::getEnabledFlag, 1)
                .orderByAsc(CmsSiteLink::getSortOrder)
                .orderByAsc(CmsSiteLink::getId));
    }

    @Override
    public List<CmsSiteLink> listAll() {
        return list(new LambdaQueryWrapper<CmsSiteLink>()
                .orderByAsc(CmsSiteLink::getSortOrder)
                .orderByAsc(CmsSiteLink::getId));
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Boolean replaceAll(List<SiteLinkInput> inputList) {
        remove(new LambdaQueryWrapper<>());
        List<CmsSiteLink> siteLinks = new ArrayList<>();
        for (int i = 0; i < inputList.size(); i++) {
            SiteLinkInput input = inputList.get(i);
            CmsSiteLink siteLink = BeanUtil.copyProperties(input, CmsSiteLink.class);
            siteLink.setId(null);
            siteLink.setSortOrder(input.getSortOrder() == null ? i + 1 : input.getSortOrder());
            siteLink.setEnabledFlag(input.getEnabledFlag() == null ? 1 : input.getEnabledFlag());
            siteLinks.add(siteLink);
        }
        return siteLinks.isEmpty() || saveBatch(siteLinks);
    }
}
